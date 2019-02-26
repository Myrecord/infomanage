/*
  Highcharts JS v7.0.1 (2018-12-19)

 Indicator series type for Highstock

 (c) 2010-2018 Pawe Fus

 License: www.highcharts.com/license
*/
(function(e){"object"===typeof module&&module.exports?module.exports=e:"function"===typeof define&&define.amd?define(function(){return e}):e("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(e){var A=function(b){var l=b.each,e=b.merge,p=b.error,q=b.defined,m=b.seriesTypes.sma;return{pointArrayMap:["top","bottom"],pointValKey:"top",linesApiNames:["bottomLine"],getTranslatedLinesNames:function(a){var c=[];l(this.pointArrayMap,function(d){d!==a&&c.push("plot"+d.charAt(0).toUpperCase()+d.slice(1))});
return c},toYData:function(a){var c=[];l(this.pointArrayMap,function(d){c.push(a[d])});return c},translate:function(){var a=this,c=a.pointArrayMap,d=[],b,d=a.getTranslatedLinesNames();m.prototype.translate.apply(a,arguments);l(a.points,function(m){l(c,function(c,f){b=m[c];null!==b&&(m[d[f]]=a.yAxis.toPixels(b,!0))})})},drawGraph:function(){var a=this,c=a.linesApiNames,d=a.points,b=d.length,r=a.options,z=a.graph,f={options:{gapSize:r.gapSize}},g=[],h=a.getTranslatedLinesNames(a.pointValKey),k;l(h,
function(a,c){for(g[c]=[];b--;)k=d[b],g[c].push({x:k.x,plotX:k.plotX,plotY:k[a],isNull:!q(k[a])});b=d.length});l(c,function(b,c){g[c]?(a.points=g[c],r[b]?a.options=e(r[b].styles,f):p('Error: "There is no '+b+' in DOCS options declared. Check if linesApiNames are consistent with your DOCS line names." at mixin/multiple-line.js:34'),a.graph=a["graph"+b],m.prototype.drawGraph.call(a),a["graph"+b]=a.graph):p('Error: "'+b+" doesn't have equivalent in pointArrayMap. To many elements in linesApiNames relative to pointArrayMap.\"")});
a.points=d;a.options=r;a.graph=z;m.prototype.drawGraph.call(a)}}}(e);(function(b,e){var l=b.merge,p=b.isArray,q=b.seriesTypes.sma;b.seriesType("bb","sma",{params:{period:20,standardDeviation:2,index:3},bottomLine:{styles:{lineWidth:1,lineColor:void 0}},topLine:{styles:{lineWidth:1,lineColor:void 0}},tooltip:{pointFormat:'\x3cspan style\x3d"color:{point.color}"\x3e\u25cf\x3c/span\x3e\x3cb\x3e {series.name}\x3c/b\x3e\x3cbr/\x3eTop: {point.top}\x3cbr/\x3eMiddle: {point.middle}\x3cbr/\x3eBottom: {point.bottom}\x3cbr/\x3e'},
marker:{enabled:!1},dataGrouping:{approximation:"averages"}},b.merge(e,{pointArrayMap:["top","middle","bottom"],pointValKey:"middle",nameComponents:["period","standardDeviation"],linesApiNames:["topLine","bottomLine"],init:function(){q.prototype.init.apply(this,arguments);this.options=l({topLine:{styles:{lineColor:this.color}},bottomLine:{styles:{lineColor:this.color}}},this.options)},getValues:function(b,a){var c=a.period,d=a.standardDeviation,e=b.xData,l=(b=b.yData)?b.length:0,m=[],f,g,h,k,v=[],
w=[],x,n;if(e.length<c)return!1;x=p(b[0]);for(n=c;n<=l;n++){k=e.slice(n-c,n);g=b.slice(n-c,n);f=q.prototype.getValues.call(this,{xData:k,yData:g},a);k=f.xData[0];f=f.yData[0];h=0;for(var y=g.length,t=0,u;t<y;t++)u=(x?g[t][a.index]:g[t])-f,h+=u*u;h=Math.sqrt(h/(y-1));g=f+d*h;h=f-d*h;m.push([k,g,f,h]);v.push(k);w.push([g,f,h])}return{values:m,xData:v,yData:w}}}))})(e,A)});
//# sourceMappingURL=bollinger-bands.js.map
