import os
from datasets import load_dataset, concatenate_datasets
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, DataCollatorForSeq2Seq
import torch
import json

# Constantes
folder = "output/dataset"
max_input_length = 1024
max_target_length = 512

def preprocess(batch, tokenizer):
    inputs = tokenizer(batch["input"], truncation=True, padding="max_length", max_length=max_input_length)
    targets = tokenizer(batch["target"], truncation=True, padding="max_length", max_length=max_target_length)
    batch["input_ids"] = inputs["input_ids"]
    batch["attention_mask"] = inputs["attention_mask"]
    batch["labels"] = targets["input_ids"]
    return batch

def main():
    # Concatenando datasets
    print("Carregando dataset...\n")
    data_files = {"train": [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".jsonl")]}
    dataset = load_dataset("json", data_files=data_files)["train"]
    dataset = dataset.filter(lambda x: x["target"].strip() != "")


    print(f"Dataset carregado com {len(dataset)} arquivos.\n")
    print(f"Primeiro arquivo do dataset: {dataset[0]}\n")


    # Split treino/validação (80/20)
    print("Separando dataset...\n")
    split = dataset.train_test_split(test_size=0.2)
    train_dataset = split["train"]
    val_dataset = split["test"]
    print(f"Dataset de treino com {len(train_dataset)} arquivos.\n")
    print(f"Dataset de validação com {len(val_dataset)} arquivos.\n")

    # Modelo e tokenizer
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to("cuda")

    # Tokenização
    train_dataset = train_dataset.map(lambda batch: preprocess(batch, tokenizer), batched=True)
    val_dataset = val_dataset.map(lambda batch: preprocess(batch, tokenizer), batched=True)

    # Data collator
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    # Argumentos de treinamento
    training_args = TrainingArguments(
        output_dir="output/t5_finetuned",
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        learning_rate=5e-5,
        num_train_epochs=3,
        logging_steps=10,
        save_strategy="epoch",
        eval_strategy="epoch",
        save_total_limit=2,
        fp16=True,
    )

    # Treinador
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator
    )

    print("Iniciando treinamento...\n")
    # Treinar
    trainer.train()

if __name__ == "__main__":
    main()
