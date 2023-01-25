from abc import ABC, abstractmethod
from pympler import asizeof

from abstract_classes.plotter_abstract import PlotterAbstract


markdown_text = str


class ReportPlotterAbstract(ABC):

    def __init__(self, plotter: PlotterAbstract, markdown_plots_list: list[markdown_text]):
        self.plotter = plotter
        self.plots_directory = plotter.plots_directory
        self.markdown_plots_list = markdown_plots_list

    def get_plot_markdown_text(self, file_name: str) -> tuple[str, markdown_text]:
        plot_path = f'{self.plots_directory}/{file_name}.png'
        plot_name = f"{plot_path.split('/')[-1]}"
        plot_markdown = f"![image]({plot_path})"
        return plot_name, plot_markdown

    @abstractmethod
    def make_plots(self) -> None:
        pass

    def get_size(self) -> str:
        size_in_mb = asizeof.asizeof(self) / 1024 / 1024
        return f'{str(self).split("(")[0]} object size is {size_in_mb:.2f} Mb'
