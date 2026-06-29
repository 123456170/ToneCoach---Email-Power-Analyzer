# report_builder.py
def build_full_report(email_data, tone_results, sentences, target_register):
    report = f"""# ToneCoach Analysis Report
Email Effectiveness: {tone_results['overall_score']}/100

## Key Dimensions
"""
    for dim, data in tone_results["dimensions"].items():
        report += f"- {dim.title()}: {data['score']}/100 ({data['label']})\n"
    
    report += "\n## Recommendations\n1. Reduce hedging phrases\n2. Increase ownership language\n3. Strengthen calls to action\n"
    return report