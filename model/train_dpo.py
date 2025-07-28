import argparse, json, os
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from trl import DPOTrainer, DPOConfig

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--model_name_or_path', required=True)
    p.add_argument('--dataset_path', required=True, help='JSONL with prompt/chosen/rejected')
    p.add_argument('--output_dir', required=True)
    p.add_argument('--epochs', type=int, default=1)
    return p.parse_args()

def main():
    args = parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, use_fast=True)
    tokenizer.pad_token = tokenizer.eos_token

    ds = load_dataset('json', data_files=args.dataset_path, split='train')

    cfg = DPOConfig(
        beta=0.1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        num_train_epochs=args.epochs,
        learning_rate=1e-5,
        max_length=512,
        output_dir=args.output_dir,
    )

    model = AutoModelForCausalLM.from_pretrained(
        args.model_name_or_path,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map='auto'
    )

    trainer = DPOTrainer(
        model=model,
        args=TrainingArguments(output_dir=args.output_dir, learning_rate=1e-5, num_train_epochs=args.epochs),
        tokenizer=tokenizer,
        beta=cfg.beta,
        train_dataset=ds,
    )
    trainer.train()
    trainer.save_model(args.output_dir)

if __name__ == '__main__':
    main()
