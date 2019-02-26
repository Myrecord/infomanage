/*
  Highcharts JS v7.0.1 (2018-12-19)

 Indicator series type for Highstock

 (c) 2010-2018 Wojciech Chmiel

 License: www.highcharts.com/license
*/
(function(e){"object"===typeof module&&module.exports?module.exports=e:"function"===typeof define&&define.amd?define(function(){return e}):e("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(e){var m=function(c){var g=c.each,q=c.merge,h=c.error,d=c.defined,b=c.seriesTypes.sma;return{pointArrayMap:["top","bottom"],pointValKey:"top",linesApiNames:["bottomLine"],getTranslatedLinesNames:function(a){var b=[];g(this.pointArrayMap,function(f){f!==a&&b.push("plot"+f.charAt(0).toUpperCase()+f.slice(1))});
return b},toYData:function(a){var b=[];g(this.pointArrayMap,function(f){b.push(a[f])});return b},translate:function(){var a=this,d=a.pointArrayMap,f=[],k,f=a.getTranslatedLinesNames();b.prototype.translate.apply(a,arguments);g(a.points,function(b){g(d,function(d,c){k=b[d];null!==k&&(b[f[c]]=a.yAxis.toPixels(k,!0))})})},drawGraph:function(){var a=this,c=a.linesApiNames,f=a.points,k=f.length,e=a.options,m=a.graph,p={options:{gapSize:e.gapSize}},n=[],r=a.getTranslatedLinesNames(a.pointValKey),l;g(r,
function(a,b){for(n[b]=[];k--;)l=f[k],n[b].push({x:l.x,plotX:l.plotX,plotY:l[a],isNull:!d(l[a])});k=f.length});g(c,function(d,f){n[f]?(a.points=n[f],e[d]?a.options=q(e[d].styles,p):h('Error: "There is no '+d+' in DOCS options declared. Check if linesApiNames are consistent with your DOCS line names." at mixin/multiple-line.js:34'),a.graph=a["graph"+d],b.prototype.drawGraph.call(a),a["graph"+d]=a.graph):h('Error: "'+d+" doesn't have equivalent in pointArrayMap. To many elements in linesApiNames relative to pointArrayMap.\"")});
a.points=f;a.options=e;a.graph=m;b.prototype.drawGraph.call(a)}}}(e),p=function(c){var e=c.error;return{isParentLoaded:function(c,h,d,b,a){if(c)return b?b(c):!0;e(a||this.generateMessage(d,h));return!1},generateMessage:function(c,e){return'Error: "'+c+'" indicator type requires "'+e+'" indicator loaded before. Please read docs: https://api.highcharts.com/highstock/plotOptions.'+c}}}(e);(function(c,e,m){var h=c.seriesTypes.aroon;c.seriesType("aroonoscillator","aroon",{params:{period:25},tooltip:{pointFormat:'\x3cspan style\x3d"color:{point.color}"\x3e\u25cf\x3c/span\x3e\x3cb\x3e {series.name}\x3c/b\x3e: {point.y}'}},
c.merge(e,{nameBase:"Aroon Oscillator",pointArrayMap:["y"],pointValKey:"y",linesApiNames:[],init:function(){var d=arguments,b=this;m.isParentLoaded(h,"aroon",b.type,function(a){a.prototype.init.apply(b,d)})},getValues:function(d,b){var a=[],c=[],f=[],e,g;d=h.prototype.getValues.call(this,d,b);for(b=0;b<d.yData.length;b++)e=d.yData[b][0],g=d.yData[b][1],e-=g,a.push([d.xData[b],e]),c.push(d.xData[b]),f.push(e);return{values:a,xData:c,yData:f}}}))})(e,m,p)});
//# sourceMappingURL=aroon-oscillator.js.map
