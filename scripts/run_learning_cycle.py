from evolution.learning_pipeline import LearningPipeline

def main():
    pipeline = LearningPipeline()
    result = pipeline.run_learning_cycle()
    print(f"Learning cycle finished. Recommendations generated: {result['recommendations_generated']}")

if __name__ == "__main__":
    main()
