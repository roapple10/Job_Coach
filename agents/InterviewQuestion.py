from AiEngine import AiEngine
from Candidate import Candidate
from Job import Job
from agents.BaseAiEngineAgent import BaseAiEngineAgent


class InterviewQuestion(BaseAiEngineAgent):
    def __init__(self, ai: AiEngine, candidate: Candidate, job: Job, additional_guidance=None, is_rewrite=False, use_writing_style: bool = True):
            role = 'Interviewer'

            background = """
                You are skilled in conducting interviews for various job roles.
                You are adept at formulating relevant questions based on the candidate's resume and the job description.
                You focus on uncovering the candidate's strengths, experiences, and suitability for the role.
                You ensure that your questions are insightful and aimed at evaluating the candidate's fit for the job.
            """

            goal = 'Generate relevant questions for the candidate based on their resume and the job description.'

            context = {
                'job_description': job.job_description,
                'job_title': job.job_title,
                'company_name': job.company_name,
                'hiring_manager': job.hiring_manager,
                'source': job.source,
                'key_required_skills': job.top_required_skills.keys(),
                'candidate_strengths': job.strengths.keys(),
                'candidate_name': candidate.candidate_name,
                'candidates_resume': candidate.resume_text,
            }

            instructions = self.get_instructions()

            if additional_guidance is not None and len(additional_guidance) > 0:
                instructions += f'\n\nIn addition to the provided instructions, here is some additional guidance: {additional_guidance}'

            output_format = """
                The output should consist of 5 relevant questions.
                Each question should be specific and tailored to the candidate's resume and the job role.
                The questions should explore the candidate's experiences, achievements, and specific skills relevant to the job.
                """

            super().__init__(ai, role, goal, background, context, instructions, output_format=output_format)

    @staticmethod
    def get_instructions() -> str:
        return """
            You have developed the following process for generating insightful interview questions:
            1. Review the job_title, company_name, hiring_manager, source, and job_description.
            2. Examine the candidate's resume closely, focusing on the experiences and skills listed.
            3. Identify areas where the candidate's background aligns with the job's key requirements.
            4. Formulate questions that probe deeper into these areas, assessing the candidate's capabilities and fit for the role.
            5. Ensure that the questions are open-ended to allow the candidate to provide detailed responses.
        """

