from laboratory.research_memory import ResearchMemory
from laboratory.future_predictor import FuturePredictor

def main():
    memory = ResearchMemory()
    predictor = FuturePredictor(memory)
    
    print("Technical debt is rising. Running Future Predictor...")
    # Current debt is 80, rising by 2 per day, predicting 30 days out
    prediction = predictor.predict("technical_debt", 80.0, 2.0, 30)
    
    print(f"\nPrediction ID: {prediction['id']}")
    print(f"Metric: {prediction['metric']}")
    print(f"Predicted Value in 30 days: {prediction['predicted_value']}")
    print(f"Confidence: {prediction['confidence']:.2f}")
    
    warnings = predictor.generate_warnings([prediction])
    if warnings:
        print("\n*** CRITICAL WARNING ***")
        for w in warnings:
            print(w)
            
    print("\n=> Optimization plan generated to address risk.")

if __name__ == "__main__":
    main()
