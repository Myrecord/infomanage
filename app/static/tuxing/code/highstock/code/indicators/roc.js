/*
  Highcharts JS v7.0.1 (2018-12-19)

 Indicator series type for Highstock

 (c) 2010-2018 Kacper Madej

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?module.exports=a:"function"===typeof define&&define.amd?define(function(){return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){(function(a){var f=a.seriesType,m=a.isArray;f("roc","sma",{params:{index:3,period:9}},{nameBase:"Rate of Change",getValues:function(d,c){var a=c.period,g=d.xData,f=(d=d.yData)?d.length:0,h=[],k=[],l=[],e=-1,b;if(g.length<=a)return!1;m(d[0])&&(e=c.index);for(c=a;c<f;c++)b=0>e?(b=d[c-a])?(d[c]-b)/
b*100:null:(b=d[c-a][e])?(d[c][e]-b)/b*100:null,b=[g[c],b],h.push(b),k.push(b[0]),l.push(b[1]);return{values:h,xData:k,yData:l}}})})(a)});
//# sourceMappingURL=roc.js.map
