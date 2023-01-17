from activity_stage.activity_stage_plotter import ActivityStagePlotter


class ActivityStageReportPlotter:
    plots_directory = './mifit_analyzer/plots/'

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16
    plot_figsize = (12, 8)

    def __init__(self, plotter: ActivityStagePlotter, markdown_plots_list: list[str]):
        self.plotter = plotter
        self.markdown_plots_list = markdown_plots_list

    def get_plot_markdown_text(self, file_name: str) -> tuple[str, str]:
        plot_path = f'{self.plots_directory}/{file_name}.png'
        plot_name = f"{plot_path.split('/')[-1]}"
        plot_markdown = f"![image]({plot_path})"
        return plot_name, plot_markdown

    def make_activity_stage_plots(self) -> None:
        self.markdown_plots_list.append('Here you can find your activity stage plots\n')

        self._make_activity_stage_km_h_plots()
        self._make_activity_stage_scatterplots()

    def _make_activity_stage_km_h_plots(self) -> None:
        self.plotter.make_activity_stage_histplot_km_h()
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_stage_histplot_km_h'))

    def _make_activity_stage_scatterplots(self) -> None:
        self.plotter.make_activity_stage_start_stop_hour_per_weekday_scatterplot()
        self.markdown_plots_list.extend(self.get_plot_markdown_text(
            'activity_stage_start_stop_hour_per_weekday_scatterplot'))

        self.plotter.make_activity_stage_start_hour_and_steps_per_weekday_scatterplot()
        self.markdown_plots_list.extend(self.get_plot_markdown_text(
            'activity_stage_start_hour_and_steps_per_weekday_scatterplot'))
