from tethys_sdk.base import TethysAppBase, url_map_maker


class Streamflownepal(TethysAppBase):
    """
    Tethys app class for Streamflownepal.
    """

    name = 'ECMWF Streamflow Prediction Tool - Nepal'
    index = 'streamflownepal:home'
    icon = 'streamflownepal/images/icon.gif'
    package = 'streamflownepal'
    root_url = 'streamflownepal'
    color = '#16a085'
    description = ''
    tags = 'ECMWF Streamflow Prediction'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='streamflownepal',
                controller='streamflownepal.controllers.index'),
            UrlMap(
                name='chart',
                url='streamflownepal/chart',
                controller='streamflownepal.controllers.chart'),
            UrlMap(
                name='forecastpercent',
                url='streamflownepal/forecastpercent',
                controller='streamflownepal.controllers.forecastpercent'),
            UrlMap(
                name='getFeatures',
                url='streamflownepal/api/getFeatures',
                controller='streamflownepal.api.getFeatures'),
            UrlMap(
                name='getreturnPeriod',
                url='streamflownepal/api/getreturnPeriod',
                controller='streamflownepal.api.getreturnPeriod'),
            UrlMap(
                name='getHistoric',
                url='streamflownepal/api/getHistoric',
                controller='streamflownepal.api.getHistoric'),
            UrlMap(
                name='getFlowDurationCurve',
                url='streamflownepal/api/getFlowDurationCurve',
                controller='streamflownepal.api.getFlowDurationCurve'),
            UrlMap(
                name='getForecast',
                url='streamflownepal/api/getForecast',
                controller='streamflownepal.api.getForecast'),
            UrlMap(
                name='getForecastCSV',
                url='streamflownepal/getForecastCSV',
                controller='streamflownepal.controllers.getForecastCSV'),
            UrlMap(
                name='getHistoricCSV',
                url='streamflownepal/getHistoricCSV',
                controller='streamflownepal.controllers.getHistoricCSV'),
        )
        return url_maps
