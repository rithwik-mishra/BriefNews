from datasets import load_dataset
from evaluate import load as load_metric
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
import numpy as np

# Load the CNN/Daily Mail "test" dataset and split into train and test
dataset = load_dataset("abisee/cnn_dailymail", "3.0.0", split="test")
dataset = dataset.train_test_split(test_size=0.2, shuffle=True) # type: ignore

tokenizer = AutoTokenizer.from_pretrained("google-t5/t5-small") 

# Preprocess the dataset
prefix = "summarize: "
def preprocess(data):
    # Tokenize articles with prompt prefix so T5 knows this is a summarization task
    inputs = [prefix + row for row in data["article"]]
    model_inputs = tokenizer(inputs, max_length=1024, truncation=True)

    labels = tokenizer(text_target=data["highlights"], max_length=128, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Apply preprocessing over the entire loaded dataset
tokenized_dataset = dataset.map(preprocess, batched=True)

# Create a batch of examples
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model="google-t5/t5-small")

# Compute ROUGE metric scores
rouge_metric = load_metric("rouge")
def compute_rouge(eval_pred):
    predictions, labels = eval_pred
    
    # When predict_with_generate=True, predictions come as logits
    # We need to convert them to token IDs first
    if isinstance(predictions, tuple):
        predictions = predictions[0]  # Take the first element if it's a tuple
    
    # Convert logits to token IDs by taking argmax
    predictions = np.argmax(predictions, axis=-1)
    
    # Decode the token IDs to text
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    
    # Replace -100 in the labels as we can't decode them
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    result = rouge_metric.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True)

    # Compute prediction lengths
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in predictions]
    result["gen_len"] = np.mean(prediction_lens) #type: ignore

    return {k: round(v, 4) for k, v in result.items()} #type: ignore

# Set up training arguments 
model = AutoModelForSeq2SeqLM.from_pretrained("google-t5/t5-small")

training_args = Seq2SeqTrainingArguments(
    output_dir="./summarizer_model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    num_train_epochs=1,  
    per_device_train_batch_size=1,  
    per_device_eval_batch_size=1,   
    gradient_accumulation_steps=4,  
    weight_decay=0.01,
    save_total_limit=1, 
    predict_with_generate=True,
    dataloader_pin_memory=False,    
    gradient_checkpointing=True,    
    use_cpu=True,                   
)

# Train Model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"].select(range(100)), # type: ignore
    eval_dataset=tokenized_dataset["test"].select(range(20)), # type: ignore
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_rouge,
)

trainer.train()
trainer.save_model("./summarizer_model")
