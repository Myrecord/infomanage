/*
  Highcharts JS v7.0.1 (2018-12-19)

 Indicator series type for Highstock

 (c) 2010-2018 Pawel Fus, Sebastian Bochan

 License: www.highcharts.com/license
*/
(function(e){"object"===typeof module&&module.exports?module.exports=e:"function"===typeof define&&define.amd?define(function(){return e}):e("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(e){var q=function(d){var e=d.error;return{isParentLoaded:function(d,h,k,n,f){if(d)return n?n(d):!0;e(f||this.generateMessage(k,h));return!1},generateMessage:function(d,e){return'Error: "'+d+'" indicator type requires "'+e+'" indicator loaded before. Please read docs: https://api.highcharts.com/highstock/plotOptions.'+
d}}}(e);(function(d,e){var q=d.pick,h=d.error,k=d.Series,n=d.isArray,f=d.addEvent,t=d.seriesType,r=d.seriesTypes,l=d.seriesTypes.ohlc.prototype,u=e.generateMessage;f(d.Series,"init",function(b){b=b.options;var c=b.dataGrouping;b.useOhlcData&&"highcharts-navigator-series"!==b.id&&(c&&c.enabled&&(c.approximation="ohlc"),d.extend(this,{pointValKey:l.pointValKey,keys:l.keys,pointArrayMap:l.pointArrayMap,toYData:l.toYData}))});t("sma","line",{name:void 0,tooltip:{valueDecimals:4},linkedTo:void 0,params:{index:0,
period:14}},{bindTo:{series:!0,eventName:"updatedData"},useCommonDataGrouping:!0,nameComponents:["period"],nameSuffixes:[],calculateOn:"init",requiredIndicators:[],requireIndicators:function(){var b={allLoaded:!0};this.requiredIndicators.forEach(function(c){r[c]?r[c].prototype.requireIndicators():(b.allLoaded=!1,b.needed=c)});return b},init:function(b,c){function d(){var b=(a.xData||[]).length,c=a.getValues(a.linkedParent,a.options.params)||{values:[],xData:[],yData:[]};b&&b===c.xData.length&&!a.cropped&&
!a.hasGroupedData&&a.visible&&a.points?a.updateData(c.values):(a.xData=c.xData,a.yData=c.yData,a.options.data=c.values);!1===a.bindTo.series&&(delete a.processedXData,a.isDirty=!0,a.redraw());a.isDirtyData=!1}var a=this,e=a.requireIndicators();if(!e.allLoaded)return h(u(a.type,e.needed));k.prototype.init.call(a,b,c);b.linkSeries();a.dataEventsToUnbind=[];if(!a.linkedParent)return h("Series "+a.options.linkedTo+" not found! Check `linkedTo`.",!1,b);a.dataEventsToUnbind.push(f(a.bindTo.series?a.linkedParent:
a.linkedParent.xAxis,a.bindTo.eventName,d));if("init"===a.calculateOn)d();else var g=f(a.chart,a.calculateOn,function(){d();g()});return a},getName:function(){var b=this.name,c=[];b||((this.nameComponents||[]).forEach(function(b,a){c.push(this.options.params[b]+q(this.nameSuffixes[a],""))},this),b=(this.nameBase||this.type.toUpperCase())+(this.nameComponents?" ("+c.join(", ")+")":""));return b},getValues:function(b,c){var d=c.period,a=b.xData;b=b.yData;var e=b.length,g=0,f=0,h=[],k=[],l=[],m=-1,p;
if(a.length<d)return!1;for(n(b[0])&&(m=c.index?c.index:0);g<d-1;)f+=0>m?b[g]:b[g][m],g++;for(c=g;c<e;c++)f+=0>m?b[c]:b[c][m],p=[a[c],f/d],h.push(p),k.push(p[0]),l.push(p[1]),f-=0>m?b[c-g]:b[c-g][m];return{values:h,xData:k,yData:l}},destroy:function(){this.dataEventsToUnbind.forEach(function(b){b()});k.prototype.destroy.call(this)}})})(e,q)});
//# sourceMappingURL=indicators.js.map
