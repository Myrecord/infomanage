/*
  Highcharts JS v7.0.1 (2018-12-19)

 Indicator series type for Highstock

 (c) 2010-2018 Pawe Fus

 License: www.highcharts.com/license
*/
(function(d){"object"===typeof module&&module.exports?module.exports=d:"function"===typeof define&&define.amd?define(function(){return d}):d("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(d){(function(d){function r(a,b){var c=a.series.pointArrayMap,h=c.length;for(m.prototype.pointClass.prototype[b].call(a);h--;)b="dataLabel"+c[h],a[b]&&a[b].element&&a[b].destroy(),a[b]=null}var t=d.defined,u=d.isArray,m=d.seriesTypes.sma;d.seriesType("pivotpoints","sma",{params:{period:28,algorithm:"standard"},
marker:{enabled:!1},enableMouseTracking:!1,dataLabels:{enabled:!0,format:"{point.pivotLine}"},dataGrouping:{approximation:"averages"}},{nameBase:"Pivot Points",pointArrayMap:"R4 R3 R2 R1 P S1 S2 S3 S4".split(" "),pointValKey:"P",toYData:function(a){return[a.P]},translate:function(){var a=this;m.prototype.translate.apply(a);a.points.forEach(function(b){a.pointArrayMap.forEach(function(c){t(b[c])&&(b["plot"+c]=a.yAxis.toPixels(b[c],!0))})});a.plotEndPoint=a.xAxis.toPixels(a.endPoint,!0)},getGraphPath:function(a){for(var b=
this,c=a.length,h=[[],[],[],[],[],[],[],[],[]],e=[],g=b.plotEndPoint,f=b.pointArrayMap.length,n,d,k;c--;){d=a[c];for(k=0;k<f;k++)n=b.pointArrayMap[k],t(d[n])&&h[k].push({plotX:d.plotX,plotY:d["plot"+n],isNull:!1},{plotX:g,plotY:d["plot"+n],isNull:!1},{plotX:g,plotY:null,isNull:!0});g=d.plotX}h.forEach(function(a){e=e.concat(m.prototype.getGraphPath.call(b,a))});return e},drawDataLabels:function(){var a=this,b=a.pointArrayMap,c,d,e,g;a.options.dataLabels.enabled&&(d=a.points.length,b.concat([!1]).forEach(function(f,
h){for(g=d;g--;)e=a.points[g],f?(e.y=e[f],e.pivotLine=f,e.plotY=e["plot"+f],c=e["dataLabel"+f],h&&(e["dataLabel"+b[h-1]]=e.dataLabel),e.dataLabels||(e.dataLabels=[]),e.dataLabels[0]=e.dataLabel=c=c&&c.element?c:null):e["dataLabel"+b[h-1]]=e.dataLabel;m.prototype.drawDataLabels.apply(a,arguments)}))},getValues:function(a,b){var c=b.period,d=a.xData,e=(a=a.yData)?a.length:0;b=this[b.algorithm+"Placement"];var g=[],f,n=[],m=[],k,q,l,p;if(d.length<c||!u(a[0])||4!==a[0].length)return!1;for(p=c+1;p<=e+
c;p+=c)q=d.slice(p-c-1,p),l=a.slice(p-c-1,p),k=q.length,f=q[k-1],l=this.getPivotAndHLC(l),l=b(l),l=g.push([f].concat(l)),n.push(f),m.push(g[l-1].slice(1));this.endPoint=q[0]+(f-q[0])/k*c;return{values:g,xData:n,yData:m}},getPivotAndHLC:function(a){var b=-Infinity,c=Infinity,d=a[a.length-1][3];a.forEach(function(a){b=Math.max(b,a[1]);c=Math.min(c,a[2])});return[(b+c+d)/3,b,c,d]},standardPlacement:function(a){var b=a[1]-a[2];return[null,null,a[0]+b,2*a[0]-a[2],a[0],2*a[0]-a[1],a[0]-b,null,null]},camarillaPlacement:function(a){var b=
a[1]-a[2];return[a[3]+1.5*b,a[3]+1.25*b,a[3]+1.1666*b,a[3]+1.0833*b,a[0],a[3]-1.0833*b,a[3]-1.1666*b,a[3]-1.25*b,a[3]-1.5*b]},fibonacciPlacement:function(a){var b=a[1]-a[2];return[null,a[0]+b,a[0]+.618*b,a[0]+.382*b,a[0],a[0]-.382*b,a[0]-.618*b,a[0]-b,null]}},{destroyElements:function(){r(this,"destroyElements")},destroy:function(){r(this,"destroyElements")}})})(d)});
//# sourceMappingURL=pivot-points.js.map
