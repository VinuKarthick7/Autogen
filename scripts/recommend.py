from evolution.recommendation_engine import RecommendationEngine

def main():
    engine = RecommendationEngine()
    recs = engine.generate_recommendations()
    for rec in recs:
        print(f"Recommend: {rec['title']} - {rec['description']}")

if __name__ == "__main__":
    main()
