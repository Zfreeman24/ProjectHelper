from abc import ABC, abstractmethod

class ProjectServiceInterface(ABC):
    @abstractmethod
    def generate_project_idea(self, language, skills, technologies):
        """
        Generate a project idea and README content based on specified parameters.
        """
        pass

    @abstractmethod
    def create_repository(self, repo_name, readme_content, token):
        """
        Create a GitHub repository with the given README content.
        """
        pass
