/**
 * @license  Highcharts JS v7.0.1 (2018-12-19)
 *
 * Indicator series type for Highstock
 *
 * (c) 2010-2018 Rafał Sebestjański
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
	var requiredIndicatorMixin = (function (H) {
		/**
		 * (c) 2010-2018 Daniel Studencki
		 *
		 * License: www.highcharts.com/license
		 */


		var error = H.error;

		var requiredIndicatorMixin = {
		    /**
		     * Check whether given indicator is loaded, else throw error.
		     * @param {function} indicator Indicator constructor function.
		     * @param {string} requiredIndicator required indicator type.
		     * @param {string} type Type of indicator where function was called (parent).
		     * @param {function} callback Callback which is triggered if the given
		     *                            indicator is loaded. Takes indicator as
		     *                            an argument.
		     * @param {string} errMessage Error message that will be logged in console.
		     * @returns {boolean} Returns false when there is no required indicator loaded.
		     */
		    isParentLoaded: function (
		        indicator,
		        requiredIndicator,
		        type,
		        callback,
		        errMessage
		    ) {
		        if (indicator) {
		            return callback ? callback(indicator) : true;
		        }
		        error(
		            errMessage || this.generateMessage(type, requiredIndicator)
		        );
		        return false;
		    },
		    generateMessage: function (indicatorType, required) {
		        return 'Error: "' + indicatorType +
		            '" indicator type requires "' + required +
		            '" indicator loaded before. Please read docs: ' +
		            'https://api.highcharts.com/highstock/plotOptions.' +
		            indicatorType;
		    }
		};

		return requiredIndicatorMixin;
	}(Highcharts));
	(function (H, requiredIndicatorMixin) {
		/* *
		 *
		 *  License: www.highcharts.com/license
		 *
		 * */



		var isArray = H.isArray,
		    EMAindicator = H.seriesTypes.ema,
		    requiredIndicator = requiredIndicatorMixin,
		    correctFloat = H.correctFloat;

		/**
		 * The DEMA series Type
		 *
		 * @private
		 * @class
		 * @name Highcharts.seriesTypes.dema
		 *
		 * @augments Highcharts.Series
		 */
		H.seriesType('dema', 'ema',
		    /**
		     * Normalized average true range indicator (NATR). This series requires
		     * `linkedTo` option to be set and should be loaded after the
		     * `stock/indicators/indicators.js` and `stock/indicators/ema.js`.
		     *
		     * @sample {highstock} stock/indicators/dema
		     *         DEMA indicator
		     *
		     * @extends      plotOptions.ema
		     * @since        7.0.0
		     * @product      highstock
		     * @excluding    allAreas, colorAxis, compare, compareBase, joinBy, keys,
		     *               navigatorOptions, pointInterval, pointIntervalUnit,
		     *               pointPlacement, pointRange, pointStart, showInNavigator,
		     *               stacking
		     * @optionparent plotOptions.dema
		     */
		    {},
		    /**
		     * @lends Highcharts.Series#
		     */
		    {
		        init: function () {
		            var args = arguments,
		                ctx = this;

		            requiredIndicator.isParentLoaded(
		                EMAindicator,
		                'ema',
		                ctx.type,
		                function (indicator) {
		                    indicator.prototype.init.apply(ctx, args);
		                }
		            );
		        },
		        getEMA: function (
		            yVal,
		            prevEMA,
		            SMA,
		            index,
		            i,
		            xVal
		          ) {

		            return EMAindicator.prototype.calculateEma(
		                xVal || [],
		                yVal,
		                i === undefined ? 1 : i,
		                this.chart.series[0].EMApercent,
		                prevEMA,
		                index === undefined ? -1 : index,
		                SMA
		            );
		        },
		        getValues: function (series, params) {
		            var period = params.period,
		                doubledPeriod = 2 * period,
		                xVal = series.xData,
		                yVal = series.yData,
		                yValLen = yVal ? yVal.length : 0,
		                index = -1,
		                accumulatePeriodPoints = 0,
		                SMA = 0,
		                DEMA = [],
		                xDataDema = [],
		                yDataDema = [],
		                EMA = 0,
		                // EMA(EMA)
		                EMAlevel2,
		                // EMA of previous point
		                prevEMA,
		                prevEMAlevel2,
		                // EMA values array
		                EMAvalues = [],
		                i,
		                DEMAPoint;
		            series.EMApercent = (2 / (period + 1));

		            // Check period, if bigger than EMA points length, skip
		            if (yValLen < 2 * period - 1) {
		                return false;
		            }

		            // Switch index for OHLC / Candlestick / Arearange
		            if (isArray(yVal[0])) {
		                index = params.index ? params.index : 0;
		            }

		            // Accumulate first N-points
		            accumulatePeriodPoints =
		                EMAindicator.prototype.accumulatePeriodPoints(
		                    period,
		                    index,
		                    yVal
		            );

		            // first point
		            SMA = accumulatePeriodPoints / period;
		            accumulatePeriodPoints = 0;

		            // Calculate value one-by-one for each period in visible data
		            for (i = period; i < yValLen + 2; i++) {
		                if (i < yValLen + 1) {
		                    EMA = this.getEMA(
		                        yVal,
		                        prevEMA,
		                        SMA,
		                        index,
		                        i
		                    )[1];
		                    EMAvalues.push(EMA);
		                }
		                prevEMA = EMA;

		                // Summing first period points for EMA(EMA)
		                if (i < doubledPeriod) {
		                    accumulatePeriodPoints += EMA;
		                } else {
		                    // Calculate DEMA
		                    // First DEMA point
		                    if (i === doubledPeriod) {
		                        SMA = accumulatePeriodPoints / period;
		                    }
		                    EMA = EMAvalues[i - period - 1];
		                    EMAlevel2 = this.getEMA(
		                        [EMA],
		                        prevEMAlevel2,
		                        SMA
		                    )[1];
		                    DEMAPoint = [
		                        xVal[i - 2],
		                        correctFloat(2 * EMA - EMAlevel2)
		                    ];
		                    DEMA.push(DEMAPoint);
		                    xDataDema.push(DEMAPoint[0]);
		                    yDataDema.push(DEMAPoint[1]);
		                    prevEMAlevel2 = EMAlevel2;
		                }
		            }

		            return {
		                values: DEMA,
		                xData: xDataDema,
		                yData: yDataDema
		            };
		        }
		    }
		);

		/**
		 * A `DEMA` series. If the [type](#series.ema.type) option is not
		 * specified, it is inherited from [chart.type](#chart.type).
		 *
		 * @extends   series,plotOptions.ema
		 * @since     7.0.0
		 * @product   highstock
		 * @excluding allAreas, colorAxis, compare, compareBase, dataParser, dataURL,
		 *            joinBy, keys, navigatorOptions, pointInterval, pointIntervalUnit,
		 *            pointPlacement, pointRange, pointStart, showInNavigator, stacking
		 * @apioption series.dema
		 */

	}(Highcharts, requiredIndicatorMixin));
	return (function () {


	}());
}));
