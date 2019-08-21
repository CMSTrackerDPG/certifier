from django_extensions.management.jobs import MinutelyJob
from analysis.analyse import run_principal_component_analysis, run_tsne, run_umap, load_data
from analysis.models import ChartDataModel

class Job(MinutelyJob):
    help = "Chart Data Load Job"

    def execute(self):
        runs = load_data()

        pca_data = run_principal_component_analysis(runs)
        t_sne_data = run_tsne(runs)
        umap_data = run_umap(runs)

        ChartDataModel.objects.create(pca_data=pca_data.to_csv(), t_sne_data=t_sne_data.to_csv(), umap_data=umap_data.to_csv())
        import os
        os.system("notify-send baaaaaaa")
