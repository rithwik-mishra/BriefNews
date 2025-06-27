"""
Script to evaluate the trained summarizer model and display detailed metrics
"""
from datasets import load_dataset
from evaluate import load as load_metric
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
import numpy as np
import json

def load_and_preprocess_data():
    """Load and preprocess the dataset for evaluation"""
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
    
    return tokenized_dataset, tokenizer

def compute_rouge_metrics(tokenizer):
    """Define the ROUGE metric computation function"""
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
    
    return compute_rouge

def evaluate_model(model_path="./summarizer_model", num_test_samples=50):
    """Evaluate the saved model and display detailed metrics"""
    print("Loading dataset and preprocessing...")
    tokenized_dataset, tokenizer = load_and_preprocess_data()
    
    print("Loading the trained model...")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    
    # Set up training arguments for evaluation
    training_args = Seq2SeqTrainingArguments(
        output_dir="./temp_eval",
        evaluation_strategy="no",  # We'll evaluate manually
        per_device_eval_batch_size=1,
        predict_with_generate=True,
        dataloader_pin_memory=False,
        use_cpu=True,
    )
    
    # Create data collator
    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model="google-t5/t5-small")
    
    # Create trainer for evaluation
    trainer = Trainer(
        model=model,
        args=training_args,
        eval_dataset=tokenized_dataset["test"].select(range(num_test_samples)), # type: ignore
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_rouge_metrics(tokenizer),
    )
    
    print(f"\nEvaluating model on {num_test_samples} test samples...")
    eval_results = trainer.evaluate()
    
    # Display results in a formatted way
    print("\n" + "="*60)
    print("MODEL EVALUATION RESULTS")
    print("="*60)
    
    # Group metrics by type
    rouge_metrics = {k: v for k, v in eval_results.items() if k.startswith('eval_rouge')}
    other_metrics = {k: v for k, v in eval_results.items() if not k.startswith('eval_rouge')}
    
    print("\nROUGE Metrics:")
    print("-" * 30)
    for metric, value in rouge_metrics.items():
        metric_name = metric.replace('eval_', '').replace('_', ' ').title()
        print(f"{metric_name}: {value:.4f}")
    
    print("\nOther Metrics:")
    print("-" * 30)
    for metric, value in other_metrics.items():
        metric_name = metric.replace('eval_', '').replace('_', ' ').title()
        print(f"{metric_name}: {value:.4f}")
    
    # Save detailed results
    results_file = "./detailed_evaluation_results.json"
    with open(results_file, "w") as f:
        json.dump(eval_results, f, indent=2)
    
    print(f"\nDetailed results saved to: {results_file}")
    
    return eval_results

def show_sample_predictions(model_path="./summarizer_model", num_samples=3):
    """Show sample predictions from the model"""
    print("\n" + "="*60)
    print("SAMPLE PREDICTIONS")
    print("="*60)
    
    tokenized_dataset, tokenizer = load_and_preprocess_data()
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    
    # Get a few samples from the test set
    test_samples = tokenized_dataset["test"].select(range(num_samples)) # type: ignore
    
    for i, sample in enumerate(test_samples):
        print(f"\n--- Sample {i+1} ---")
        
        # Get the original article text (remove the prefix)
        article_text = sample['input_ids']  # type: ignore
        # Decode to get the original text
        input_text = tokenizer.decode(article_text, skip_special_tokens=True)
        input_text = input_text.replace("summarize: ", "")
        
        # Get the reference summary
        reference = tokenizer.decode(sample['labels'], skip_special_tokens=True)  # type: ignore
        
        # Generate prediction
        inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
        outputs = model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        print(f"Original Article (first 200 chars): {input_text[:200]}...")
        print(f"Reference Summary: {reference}")
        print(f"Model Prediction: {prediction}")
        print("-" * 50)

if __name__ == "__main__":
    # Evaluate the model
    results = evaluate_model()
    
    # Show sample predictions
    show_sample_predictions() 