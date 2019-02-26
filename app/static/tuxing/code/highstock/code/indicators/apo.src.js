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



		var EMA = H.seriesTypes.ema,
		    error = H.error,
		    requiredIndicator = requiredIndicatorMixin;

		/**
		 * The APO series type.
		 *
		 * @private
		 * @class
		 * @name Highcharts.seriesTypes.apo
		 *
		 * @augments Highcharts.Series
		 */
		H.seriesType('apo', 'ema',
		    /**
		     * Absolute Price Oscillator. This series requires the `linkedTo` option to
		     * be set and should be loaded after the `stock/indicators/indicators.js`
		     * and `stock/indicators/ema.js`.
		     *
		     * @sample {highstock} stock/indicators/apo
		     *         Absolute Price Oscillator
		     *
		     * @extends      plotOptions.ema
		     * @since        7.0.0
		     * @product      highstock
		     * @excluding    allAreas, colorAxis, joinBy, keys, navigatorOptions,
		     *               pointInterval, pointIntervalUnit, pointPlacement,
		     *               pointRange, pointStart, showInNavigator, stacking
		     * @optionparent plotOptions.apo
		     */
		    {
		        /**
		         * Paramters used in calculation of Absolute Price Oscillator
		         * series points.
		         *
		         * @excluding period
		         */
		        params: {
		            /**
		             * Periods for Absolute Price Oscillator calculations.
		             *
		             * @type    {Array<number>}
		             * @default [10, 20]
		             * @since   7.0.0
		             */
		            periods: [10, 20]
		        }
		    },
		    /**
		     * @lends Highcharts.Series.prototype
		     */
		    {
		        nameBase: 'APO',
		        nameComponents: ['periods'],
		        init: function () {
		            var args = arguments,
		                ctx = this;

		            requiredIndicator.isParentLoaded(
		                EMA,
		                'ema',
		                ctx.type,
		                function (indicator) {
		                    indicator.prototype.init.apply(ctx, args);
		                }
		            );
		        },
		        getValues: function (series, params) {
		            var periods = params.periods,
		                index = params.index,
		                APO = [], // 0- date, 1- Absolute price oscillator
		                xData = [],
		                yData = [],
		                periodsOffset,
		                SPE, // Shorter Period EMA
		                LPE, // Longer Period EMA
		                oscillator,
		                i;

		            // Check if periods are correct
		            if (periods.length !== 2 || periods[1] <= periods[0]) {
		                error(
		                    'Error: "APO requires two periods. Notice, first period ' +
		                    'should be lower than the second one."'
		                );
		                return false;
		            }

		            SPE = EMA.prototype.getValues.call(this, series, {
		                index: index,
		                period: periods[0]
		            });

		            LPE = EMA.prototype.getValues.call(this, series, {
		                index: index,
		                period: periods[1]
		            });

		            // Check if ema is calculated properly, if not skip
		            if (!SPE || !LPE) {
		                return false;
		            }

		            periodsOffset = periods[1] - periods[0];

		            for (i = 0; i < LPE.yData.length; i++) {
		                oscillator = SPE.yData[i + periodsOffset] - LPE.yData[i];

		                APO.push([LPE.xData[i], oscillator]);
		                xData.push(LPE.xData[i]);
		                yData.push(oscillator);
		            }

		            return {
		                values: APO,
		                xData: xData,
		                yData: yData
		            };
		        }
		    }
		);

		/**
		 * An `Absolute Price Oscillator` series. If the [type](#series.apo.type) option
		 * is not specified, it is inherited from [chart.type](#chart.type).
		 *
		 * @extends   series,plotOptions.apo
		 * @since     7.0.0
		 * @product   highstock
		 * @excluding allAreas, colorAxis, dataParser, dataURL, joinBy, keys,
		 *            navigatorOptions, pointInterval, pointIntervalUnit,
		 *            pointPlacement, pointRange, pointStart, showInNavigator, stacking
		 * @apioption series.apo
		 */

	}(Highcharts, requiredIndicatorMixin));
	return (function () {


	}());
}));
