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
	var multipleLinesMixin = (function (H) {
		/**
		 *
		 *  (c) 2010-2018 Wojciech Chmiel
		 *
		 *  License: www.highcharts.com/license
		 *
		 * */



		var each = H.each,
		    merge = H.merge,
		    error = H.error,
		    defined = H.defined,
		    SMA = H.seriesTypes.sma;

		/**
		 * Mixin useful for all indicators that have more than one line.
		 * Merge it with your implementation where you will provide
		 * getValues method appropriate to your indicator and pointArrayMap,
		 * pointValKey, linesApiNames properites. Notice that pointArrayMap
		 * should be consistent with amount of lines calculated in getValues method.
		 *
		 * @private
		 * @mixin multipleLinesMixin
		 */
		var multipleLinesMixin = {
		    /**
		     * Lines ids. Required to plot appropriate amount of lines.
		     * Notice that pointArrayMap should have more elements than
		     * linesApiNames, because it contains main line and additional lines ids.
		     * Also it should be consistent with amount of lines calculated in
		     * getValues method from your implementation.
		     *
		     * @private
		     * @name multipleLinesMixin.pointArrayMap
		     * @type {Array<string>}
		     */
		    pointArrayMap: ['top', 'bottom'],

		    /**
		     * Main line id.
		     *
		     * @private
		     * @name multipleLinesMixin.pointValKey
		     * @type {string}
		     */
		    pointValKey: 'top',

		    /**
		     * Additional lines DOCS names. Elements of linesApiNames array should
		     * be consistent with DOCS line names defined in your implementation.
		     * Notice that linesApiNames should have decreased amount of elements
		     * relative to pointArrayMap (without pointValKey).
		     *
		     * @private
		     * @name multipleLinesMixin.linesApiNames
		     * @type {Array<string>}
		     */
		    linesApiNames: ['bottomLine'],

		    /**
		     * Create translatedLines Collection based on pointArrayMap.
		     *
		     * @private
		     * @function multipleLinesMixin.getTranslatedLinesNames
		     *
		     * @param {string} excludedValue
		     *        pointValKey - main line id
		     *
		     * @return {Array<string>}
		     *         Returns translated lines names without excluded value.
		     */
		    getTranslatedLinesNames: function (excludedValue) {
		        var translatedLines = [];

		        each(this.pointArrayMap, function (propertyName) {
		            if (propertyName !== excludedValue) {
		                translatedLines.push(
		                    'plot' +
		                    propertyName.charAt(0).toUpperCase() +
		                    propertyName.slice(1)
		                );
		            }
		        });

		        return translatedLines;
		    },
		    /**
		     * @private
		     * @function multipleLinesMixin.toYData
		     *
		     * @param {string} point
		     *
		     * @return {Array<number>}
		     *         Returns point Y value for all lines
		     */
		    toYData: function (point) {
		        var pointColl = [];

		        each(this.pointArrayMap, function (propertyName) {
		            pointColl.push(point[propertyName]);
		        });
		        return pointColl;
		    },
		    /**
		     * Add lines plot pixel values.
		     *
		     * @private
		     * @function multipleLinesMixin.translate
		     */
		    translate: function () {
		        var indicator = this,
		            pointArrayMap = indicator.pointArrayMap,
		            LinesNames = [],
		            value;

		        LinesNames = indicator.getTranslatedLinesNames();

		        SMA.prototype.translate.apply(indicator, arguments);

		        each(indicator.points, function (point) {
		            each(pointArrayMap, function (propertyName, i) {
		                value = point[propertyName];

		                if (value !== null) {
		                    point[LinesNames[i]] = indicator.yAxis.toPixels(
		                        value,
		                        true
		                    );
		                }
		            });
		        });
		    },
		    /**
		     * Draw main and additional lines.
		     *
		     * @private
		     * @function multipleLinesMixin.drawGraph
		     */
		    drawGraph: function () {
		        var indicator = this,
		            pointValKey = indicator.pointValKey,
		            linesApiNames = indicator.linesApiNames,
		            mainLinePoints = indicator.points,
		            pointsLength = mainLinePoints.length,
		            mainLineOptions = indicator.options,
		            mainLinePath = indicator.graph,
		            gappedExtend = {
		                options: {
		                    gapSize: mainLineOptions.gapSize
		                }
		            },
		            secondaryLines = [], // additional lines point place holders
		            secondaryLinesNames = indicator.getTranslatedLinesNames(
		                pointValKey
		            ),
		            point;


		        // Generate points for additional lines:
		        each(secondaryLinesNames, function (plotLine, index) {

		            // create additional lines point place holders
		            secondaryLines[index] = [];

		            while (pointsLength--) {
		                point = mainLinePoints[pointsLength];
		                secondaryLines[index].push({
		                    x: point.x,
		                    plotX: point.plotX,
		                    plotY: point[plotLine],
		                    isNull: !defined(point[plotLine])
		                });
		            }

		            pointsLength = mainLinePoints.length;
		        });

		        // Modify options and generate additional lines:
		        each(linesApiNames, function (lineName, i) {
		            if (secondaryLines[i]) {
		                indicator.points = secondaryLines[i];
		                if (mainLineOptions[lineName]) {
		                    indicator.options = merge(
		                        mainLineOptions[lineName].styles,
		                        gappedExtend
		                    );
		                } else {
		                    error(
		                        'Error: "There is no ' + lineName +
		                        ' in DOCS options declared. Check if linesApiNames' +
		                        ' are consistent with your DOCS line names."' +
		                        ' at mixin/multiple-line.js:34'
		                    );
		                }

		                indicator.graph = indicator['graph' + lineName];
		                SMA.prototype.drawGraph.call(indicator);

		                // Now save lines:
		                indicator['graph' + lineName] = indicator.graph;
		            } else {
		                error(
		                    'Error: "' + lineName + ' doesn\'t have equivalent ' +
		                    'in pointArrayMap. To many elements in linesApiNames ' +
		                    'relative to pointArrayMap."'
		                );
		            }
		        });

		        // Restore options and draw a main line:
		        indicator.points = mainLinePoints;
		        indicator.options = mainLineOptions;
		        indicator.graph = mainLinePath;
		        SMA.prototype.drawGraph.call(indicator);
		    }
		};


		return multipleLinesMixin;
	}(Highcharts));
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
	(function (H, multipleLinesMixin, requiredIndicatorMixin) {
		/* *
		 *
		 *  License: www.highcharts.com/license
		 *
		 * */



		var AROON = H.seriesTypes.aroon,
		    requiredIndicator = requiredIndicatorMixin;

		/**
		 * The Aroon Oscillator series type.
		 *
		 * @private
		 * @class
		 * @name Highcharts.seriesTypes.aroonoscillator
		 *
		 * @augments Highcharts.Series
		 */
		H.seriesType('aroonoscillator', 'aroon',
		    /**
		     * Aroon Oscillator. This series requires the `linkedTo` option to be set
		     * and should be loaded after the `stock/indicators/indicators.js` and
		     * `stock/indicators/aroon.js`.
		     *
		     * @sample {highstock} stock/indicators/aroon-oscillator
		     *         Aroon Oscillator
		     *
		     * @extends      plotOptions.aroon
		     * @since        7.0.0
		     * @product      highstock
		     * @excluding    allAreas, aroonDown, colorAxis, compare, compareBase,
		     *               joinBy, keys, navigatorOptions, pointInterval,
		     *               pointIntervalUnit, pointPlacement, pointRange, pointStart,
		     *               showInNavigator, stacking
		     * @optionparent plotOptions.aroonoscillator
		     */
		    {
		        /**
		         * Paramters used in calculation of aroon oscillator series points.
		         *
		         * @excluding periods, index
		         */
		        params: {
		            /**
		             * Period for Aroon Oscillator
		             *
		             * @since   7.0.0
		             * @product highstock
		             */
		            period: 25
		        },
		        tooltip: {
		            pointFormat: '<span style="color:{point.color}">\u25CF</span><b> {series.name}</b>: {point.y}'
		        }
		    },
		    /**
		     * @lends Highcharts.Series#
		     */
		    H.merge(multipleLinesMixin, {
		        nameBase: 'Aroon Oscillator',
		        pointArrayMap: ['y'],
		        pointValKey: 'y',
		        linesApiNames: [],
		        init: function () {
		            var args = arguments,
		                ctx = this;

		            requiredIndicator.isParentLoaded(
		                AROON,
		                'aroon',
		                ctx.type,
		                function (indicator) {
		                    indicator.prototype.init.apply(ctx, args);
		                }
		            );
		        },
		        getValues: function (series, params) {
		            var ARO = [], // 0- date, 1- Aroon Oscillator
		                xData = [],
		                yData = [],
		                aroon,
		                aroonUp,
		                aroonDown,
		                oscillator,
		                i;

		            aroon = AROON.prototype.getValues.call(this, series, params);

		            for (i = 0; i < aroon.yData.length; i++) {
		                aroonUp = aroon.yData[i][0];
		                aroonDown = aroon.yData[i][1];
		                oscillator = aroonUp - aroonDown;

		                ARO.push([aroon.xData[i], oscillator]);
		                xData.push(aroon.xData[i]);
		                yData.push(oscillator);
		            }

		            return {
		                values: ARO,
		                xData: xData,
		                yData: yData
		            };
		        }
		    })
		);

		/**
		 * An `Aroon Oscillator` series. If the [type](#series.aroonoscillator.type)
		 * option is not specified, it is inherited from [chart.type](#chart.type).
		 *
		 * @extends   series,plotOptions.aroonoscillator
		 * @since     7.0.0
		 * @product   highstock
		 * @excluding allAreas, aroonDown, colorAxis, compare, compareBase, dataParser,
		 *            dataURL, joinBy, keys, navigatorOptions, pointInterval,
		 *            pointIntervalUnit, pointPlacement, pointRange, pointStart,
		 *            showInNavigator, stacking
		 * @apioption series.aroonoscillator
		 */

	}(Highcharts, multipleLinesMixin, requiredIndicatorMixin));
	return (function () {


	}());
}));
