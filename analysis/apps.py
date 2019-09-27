from django.apps import AppConfig


class AnalysisConfig(AppConfig):
    name = 'analysis'
    def ready(self):
        from analysis.jobs.chart_data_load_job import start_scheduler
        start_scheduler()
