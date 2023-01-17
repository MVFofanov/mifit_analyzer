from activity.activity_plotter import ActivityPlotter


class ActivityReportPlotter:
    plots_directory = './mifit_analyzer/plots/'

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16
    plot_figsize = (12, 8)

    def __init__(self, plotter: ActivityPlotter, markdown_plots_list: list[str]):
        self.plotter = plotter
        self.markdown_plots_list = markdown_plots_list

    def get_plot_markdown_text(self, file_name: str) -> tuple[str, str]:
        plot_path = f'{self.plots_directory}/{file_name}.png'
        plot_name = f"{plot_path.split('/')[-1]}"
        plot_markdown = f"![image]({plot_path})"
        return plot_name, plot_markdown

    def make_activity_plots(self) -> None:
        self.markdown_plots_list.append('Here you can find your activity plots\n')

        self._make_activity_distance_common_plots()
        self._make_activity_distance_boxplots()
        self._make_activity_steps_boxplots()

    def _make_activity_distance_common_plots(self) -> None:
        self.plotter.make_activity_pairplot()
        self.plotter.make_activity_boxplot()
        self.plotter.make_activity_steps_distance_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your common activity plots\n',
                                         *self.get_plot_markdown_text('activity_pairplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_distance_scatterplot'))

    def _make_activity_distance_boxplots(self) -> None:
        self.plotter.make_activity_distance_per_weekday_boxplot()
        self.plotter.make_activity_distance_per_month_boxplot()
        self.plotter.make_activity_distance_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your activity distance boxplots\n',
                                         *self.get_plot_markdown_text('activity_distance_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_distance_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_distance_per_year_boxplot'))

    def _make_activity_steps_boxplots(self) -> None:
        self.plotter.make_activity_steps_per_weekday_boxplot()
        self.plotter.make_activity_steps_per_month_boxplot()
        self.plotter.make_activity_steps_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your activity steps boxplots\n',
                                         *self.get_plot_markdown_text('activity_steps_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_per_year_boxplot'))
