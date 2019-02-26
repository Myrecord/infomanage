/**
 * @license  Highcharts JS v7.0.1 (2018-12-19)
 *
 * Indicator series type for Highstock
 *
 * (c) 2010-2018 Wojciech Chmiel
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
	var reduceArrayMixin = (function (H) {
		/**
		 * (c) 2010-2018 Pawel Fus & Daniel Studencki
		 *
		 * License: www.highcharts.com/license
		 */


		var reduce = H.reduce;

		var reduceArrayMixin = {
		    /**
		     * Get min value of array filled by OHLC data.
		     * @param {array} arr Array of OHLC points (arrays).
		     * @param {string} index Index of "low" value in point array.
		     * @returns {number} Returns min value.
		     */
		    minInArray: function (arr, index) {
		        return reduce(arr, function (min, target) {
		            return Math.min(min, target[index]);
		        }, Number.MAX_VALUE);
		    },
		    /**
		     * Get max value of array filled by OHLC data.
		     * @param {array} arr Array of OHLC points (arrays).
		     * @param {string} index Index of "high" value in point array.
		     * @returns {number} Returns max value.
		     */
		    maxInArray: function (arr, index) {
		        return reduce(arr, function (min, target) {
		            return Math.max(min, target[index]);
		        }, -Number.MAX_VALUE);
		    },
		    /**
		     * Get extremes of array filled by OHLC data.
		     * @param {array} arr Array of OHLC points (arrays).
		     * @param {string} minIndex Index of "low" value in point array.
		     * @param {string} maxIndex Index of "high" value in point array.
		     * @returns {array} Returns array with min and max value.
		     */
		    getArrayExtremes: function (arr, minIndex, maxIndex) {
		        return reduce(arr, function (prev, target) {
		            return [
		                Math.min(prev[0], target[minIndex]),
		                Math.max(prev[1], target[maxIndex])
		            ];
		        }, [Number.MAX_VALUE, -Number.MAX_VALUE]);
		    }
		};

		return reduceArrayMixin;
	}(Highcharts));
	(function (H, reduceArrayMixin) {
		/* *
		 *
		 *  License: www.highcharts.com/license
		 *
		 * */



		var isArray = H.isArray,
		    getArrayExtremes = reduceArrayMixin.getArrayExtremes;

		/**
		 * The Williams %R series type.
		 *
		 * @private
		 * @class
		 * @name Highcharts.seriesTypes.williamsr
		 *
		 * @augments Highcharts.Series
		 */
		H.seriesType('williamsr', 'sma',
		    /**
		     * Williams %R. This series requires the `linkedTo` option to be
		     * set and should be loaded after the `stock/indicators/indicators.js`.
		     *
		     * @sample {highstock} stock/indicators/williams-r
		     *         Williams %R
		     *
		     * @extends      plotOptions.sma
		     * @since        7.0.0
		     * @product      highstock
		     * @excluding    allAreas, colorAxis, joinBy, keys, navigatorOptions,
		     *               pointInterval, pointIntervalUnit, pointPlacement,
		     *               pointRange, pointStart, showInNavigator, stacking
		     * @optionparent plotOptions.williamsr
		     */
		    {
		        /**
		         * Paramters used in calculation of Williams %R series points.
		         * @excluding index
		         */
		        params: {
		            /**
		             * Period for Williams %R oscillator
		             */
		            period: 14
		        }
		    },
		    /**
		     * @lends Highcharts.Series#
		     */
		    {
		        nameBase: 'Williams %R',
		        getValues: function (series, params) {
		            var period = params.period,
		                xVal = series.xData,
		                yVal = series.yData,
		                yValLen = yVal ? yVal.length : 0,
		                WR = [], // 0- date, 1- Williams %R
		                xData = [],
		                yData = [],
		                slicedY,
		                close = 3,
		                low = 2,
		                high = 1,
		                extremes,
		                R,
		                HH, // Highest high value in period
		                LL, // Lowest low value in period
		                CC, // Current close value
		                i;

		            // Williams %R requires close value
		            if (
		                xVal.length < period ||
		                !isArray(yVal[0]) ||
		                yVal[0].length !== 4
		            ) {
		                return false;
		            }

		            // For a N-period, we start from N-1 point, to calculate Nth point
		            // That is why we later need to comprehend slice() elements list
		            // with (+1)
		            for (i = period - 1; i < yValLen; i++) {
		                slicedY = yVal.slice(i - period + 1, i + 1);
		                extremes = getArrayExtremes(slicedY, low, high);

		                LL = extremes[0];
		                HH = extremes[1];
		                CC = yVal[i][close];

		                R = ((HH - CC) / (HH - LL)) * -100;

		                if (xVal[i]) {
		                    WR.push([xVal[i], R]);
		                    xData.push(xVal[i]);
		                    yData.push(R);
		                }
		            }

		            return {
		                values: WR,
		                xData: xData,
		                yData: yData
		            };
		        }
		    }
		);

		/**
		 * A `Williams %R Oscillator` series. If the [type](#series.williamsr.type)
		 * option is not specified, it is inherited from [chart.type](#chart.type).
		 *
		 * @extends   series,plotOptions.williamsr
		 * @since     7.0.0
		 * @product   highstock
		 * @excluding allAreas, colorAxis, dataParser, dataURL, joinBy, keys,
		 *            navigatorOptions, pointInterval, pointIntervalUnit,
		 *            pointPlacement, pointRange, pointStart, showInNavigator, stacking
		 * @apioption series.williamsr
		 */

	}(Highcharts, reduceArrayMixin));
	return (function () {


	}());
}));
