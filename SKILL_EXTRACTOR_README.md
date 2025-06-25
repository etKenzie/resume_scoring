# Skill Extractor Agent

The Skill Extractor Agent is a specialized AI agent designed to analyze resumes and identify specific skills that are present in a candidate's background. It provides detailed skill matching analysis with context and statistics.

## Features

- **Comprehensive Skill Detection**: Analyzes resumes for both technical and soft skills
- **Context-Aware Matching**: Provides context for where each skill was found
- **Statistical Analysis**: Calculates match percentages and skill coverage
- **Flexible Input**: Accepts various skill formats and resume types
- **Integration Ready**: Works seamlessly with the existing resume scoring pipeline

## Enhanced SkillsFound Model

The agent returns a structured `SkillsFound` object with:

```python
class SkillsFound(BaseModel):
    skills_found: List[str]           # Skills actually present in resume
    total_skills_checked: int         # Total skills evaluated
    match_percentage: float           # Match rate (0.0 to 1.0)
    skill_context: List[str]          # Context for each found skill
```

## Usage Examples

### Basic Usage

```python
import asyncio
import json
from app.resume_scorer import skill_extractor_agent, Runner

async def check_skills():
    input_data = json.dumps({
        "resume_path": "path/to/resume.pdf",
        "target_skills": "Python, JavaScript, React, SQL, Leadership"
    })
    
    result = await Runner.run(skill_extractor_agent, input_data)
    
    print(f"Skills Found: {result.final_output.skills_found}")
    print(f"Match Rate: {result.final_output.match_percentage:.1%}")
    print(f"Context: {result.final_output.skill_context}")

asyncio.run(check_skills())
```

### Technical Skills Check

```python
tech_skills = "Python, JavaScript, React, Node.js, SQL, MongoDB, AWS, Docker, Git, Agile"
```

### Soft Skills Check

```python
soft_skills = "Leadership, Communication, Teamwork, Problem Solving, Time Management, Customer Service"
```

### Sales Skills Check

```python
sales_skills = "Sales, Marketing, CRM, Lead Generation, Negotiation, Account Management, Cold Calling"
```

## Integration with Resume Scoring Pipeline

The skill extractor is now integrated into the main `score_resume` function:

```python
async def score_resume(
    resume_path: str,
    job_description: str,
    skills: str,
) -> dict:
    # ... existing pipeline steps ...
    
    # Skill extraction step
    skill_extraction_input = json.dumps({
        "resume_path": resume_path,
        "target_skills": skills
    })
    
    skill_extraction_result = await Runner.run(
        skill_extractor_agent,
        skill_extraction_input
    )
    
    # ... rest of pipeline ...
    
    return {
        "skill_analysis": skills_found.model_dump(),
        "job_requirements": job_requirements.model_dump(),
        "scoring": result.model_dump(),
        "evaluation": resume_evaluation.final_output.model_dump()
    }
```

## Skill Detection Rules

The agent uses sophisticated detection rules:

1. **Exact Matches**: Direct mentions of skill names
2. **Synonyms**: Common variations (e.g., "JS" for "JavaScript")
3. **Context Clues**: Skills implied through project descriptions
4. **Certifications**: Skills mentioned in certification names

## Best Practices

### Input Format
- Provide skills as comma-separated strings
- Use standard skill names when possible
- Include both technical and soft skills for comprehensive analysis

### Expected Output
- `skills_found`: Only skills clearly demonstrated in the resume
- `match_percentage`: Accurate calculation (0.0 to 1.0)
- `skill_context`: Meaningful context for each found skill

### Error Handling
- Handles empty or malformed skill lists
- Gracefully processes different resume formats
- Provides clear error messages for debugging

## Testing

Run the provided test scripts to verify functionality:

```bash
# Basic test
python test_skill_extractor.py

# Comprehensive examples
python skill_extractor_examples.py
```

## Advanced Usage

### Custom Skill Sets
Create custom skill sets for different job roles:

```python
# Software Developer
dev_skills = "Python, Java, React, Node.js, SQL, Git, Docker, AWS, Agile, Testing"

# Data Scientist
data_skills = "Python, R, SQL, Machine Learning, Statistics, Pandas, TensorFlow, Data Visualization"

# Sales Manager
sales_skills = "Sales, CRM, Leadership, Team Management, Negotiation, Account Management, Strategy"
```

### Batch Processing
Process multiple resumes with the same skill set:

```python
async def batch_skill_check(resume_paths, target_skills):
    results = []
    for resume_path in resume_paths:
        input_data = json.dumps({
            "resume_path": resume_path,
            "target_skills": target_skills
        })
        result = await Runner.run(skill_extractor_agent, input_data)
        results.append(result.final_output)
    return results
```

## Performance Notes

- The agent processes resumes efficiently using async operations
- PDF text extraction is handled automatically
- Results are cached for better performance in batch operations
- Memory usage is optimized for large skill sets

## Troubleshooting

### Common Issues

1. **No skills found**: Check if the resume contains the target skills or if skill names need adjustment
2. **Low match percentage**: Verify skill names match common industry terminology
3. **Context missing**: Ensure the resume has sufficient detail for context extraction

### Debug Tips

- Use the test scripts to verify agent functionality
- Check resume format compatibility
- Verify skill names are spelled correctly
- Review the skill context for accuracy

## Future Enhancements

Potential improvements for the skill extractor:

- Skill confidence scoring
- Industry-specific skill recognition
- Multi-language support
- Skill level assessment (beginner, intermediate, expert)
- Integration with external skill databases 