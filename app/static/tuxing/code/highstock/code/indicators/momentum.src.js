/**
 * @license  Highcharts JS v7.0.1 (2018-12-19)
 *
 * Indicator series type for Highstock
 *
 * (c) 2010-2018 Sebastian Bochan
 *
 * License: www.highcharts.com/license
 */
'use strict';
(function (factory) {
	if (typeof module === 'object' && module.exports) {
		module.exports = factory;
	} else if (typeof define === 'function' && define.amd) {
		define(function () {
			return factory;
		});
	} else {
		factory(typeof Highcharts !== 'undefined' ? Highcharts : undefined);
	}
}(function (Highcharts) {
	(function (H) {
		/* *
		 *
		 *  License: www.highcharts.com/license
		 *
		 * */



		var isArray = H.isArray,
		    seriesType = H.seriesType;

		function populateAverage(points, xVal, yVal, i, period) {
		    var mmY = yVal[i - 1][3] - yVal[i - period - 1][3],
		        mmX = xVal[i - 1];

		    points.shift(); // remove point until range < period

		    return [mmX, mmY];
		}

		/**
		 * The Momentum series type.
		 *
		 * @private
		 * @class
		 * @name Highcharts.seriesTypes.momentum
		 *
		 * @augments Highcharts.Series
		 */
		seriesType('momentum', 'sma',
		    /**
		     * Momentum. This series requires `linkedTo` option to be set.
		     *
		     * @sample stock/indicators/momentum
		     *         Momentum indicator
		     *
		     * @extends      plotOptions.sma
		     * @since        6.0.0
		     * @product      highstock
		     * @optionparent plotOptions.momentum
		     */
		    {
		        params: {
		            period: 14
		        }
		    },
		    /**
		     * @lends Highcharts.Series#
		     */
		    {
		        nameBase: 'Momentum',
		        getValues: function (series, params) {
		            var period = params.period,
		                xVal = series.xData,
		                yVal = series.yData,
		                yValLen = yVal ? yVal.length : 0,
		                xValue = xVal[0],
		                yValue = yVal[0],
		                MM = [],
		                xData = [],
		                yData = [],
		                index,
		                i,
		                points,
		                MMPoint;

		            if (xVal.length <= period) {
		                return false;
		            }

		            // Switch index for OHLC / Candlestick / Arearange
		            if (isArray(yVal[0])) {
		                yValue = yVal[0][3];
		            } else {
		                return false;
		            }
		            // Starting point
		            points = [
		                [xValue, yValue]
		            ];


		            // Calculate value one-by-one for each period in visible data
		            for (i = (period + 1); i < yValLen; i++) {
		                MMPoint = populateAverage(points, xVal, yVal, i, period, index);
		                MM.push(MMPoint);
		                xData.push(MMPoint[0]);
		                yData.push(MMPoint[1]);
		            }

		            MMPoint = populateAverage(points, xVal, yVal, i, period, index);
		            MM.push(MMPoint);
		            xData.push(MMPoint[0]);
		            yData.push(MMPoint[1]);

		            return {
		                values: MM,
		                xData: xData,
		                yData: yData
		            };
		        }
		    }
		);

		/**
		 * A `Momentum` series. If the [type](#series.momentum.type) option is not
		 * specified, it is inherited from [chart.type](#chart.type).
		 *
		 * @extends   series,plotOptions.momentum
		 * @since     6.0.0
		 * @excluding dataParser, dataURL
		 * @product   highstock
		 * @apioption series.momentum
		 */

	}(Highcharts));
	return (function () {


	}());
}));
