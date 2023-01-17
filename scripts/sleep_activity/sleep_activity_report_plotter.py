from sleep_activity.sleep_activity_plotter import SleepActivityPlotter


class SleepActivityReportPlotter:
    plots_directory = './mifit_analyzer/plots/'

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16
    plot_figsize = (12, 8)

    def __init__(self, plotter: SleepActivityPlotter, markdown_plots_list: list[str]):
        self.plotter = plotter
        self.markdown_plots_list = markdown_plots_list

    def get_plot_markdown_text(self, file_name: str) -> tuple[str, str]:
        plot_path = f'{self.plots_directory}/{file_name}.png'
        plot_name = f"{plot_path.split('/')[-1]}"
        plot_markdown = f"![image]({plot_path})"
        return plot_name, plot_markdown

    def make_sleep_activity_plots(self) -> None:
        self.plotter.make_sleep_activity_correlations_plot()
        self.plotter.make_sleep_activity_steps_sleep_per_start_weekday_scatterplot()
        self.plotter.make_sleep_activity_steps_sleep_per_stop_weekday_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your sleep activity plots\n',
                                         *self.get_plot_markdown_text('sleep_activity_correlations_plot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_activity_steps_sleep_per_start_weekday'
                                                                    '_scatterplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_activity_steps_sleep_per_stop_weekday'
                                                                    '_scatterplot'))
