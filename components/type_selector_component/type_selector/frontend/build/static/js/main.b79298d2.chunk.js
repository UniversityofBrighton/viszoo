(this.webpackJsonpstreamlit_component_type_selector=this.webpackJsonpstreamlit_component_type_selector||[]).push([[0],{16:function(e,t,r){e.exports=r(23)},23:function(e,t,r){"use strict";r.r(t);var n=r(6),o=r.n(n),a=r(14),i=r.n(a),l=r(5),c=r(0),d=r(1),s=r(2),p=r(3),u=r(12),b=function(e){Object(s.a)(r,e);var t=Object(p.a)(r);function r(){var e;Object(d.a)(this,r);for(var n=arguments.length,a=new Array(n),i=0;i<n;i++)a[i]=arguments[i];return(e=t.call.apply(t,[this].concat(a))).state={types:e.props.args.types},e.render=function(){var t=e.state.types,r=t.map((function(r,n){var a,i,c;return i="nan"===r.name?"no type":r.name,a=!0===r.selected?"black":"lightgray",c={height:12,width:12,display:"inline-block",cursor:"pointer"},"circle"===r.shape&&(c=Object(l.a)(Object(l.a)({},c),{},{borderRadius:15,backgroundColor:a})),"triangle"===r.shape&&(c={width:0,height:0,backgroundColor:"transparent",borderStyle:"solid",borderTopWidth:0,borderLeftWidth:6,borderRightWidth:6,borderBottomWidth:12,borderLeftColor:"transparent",borderRightColor:"transparent",borderBottomColor:a,display:"inline-block",cursor:"pointer"}),"square"===r.shape&&(c=Object(l.a)(Object(l.a)({},c),{},{backgroundColor:a})),c={height:12,width:12,display:"inline-block",cursor:"pointer",backgroundColor:a},o.a.createElement("div",null,o.a.createElement("div",{style:Object(l.a)({},c),onClick:function(){return e.onClicked(t,n)}}),o.a.createElement("div",{style:{display:"inline-block",paddingLeft:10}},i))})),n=e.props.theme,a="blue",i="blue";n&&(a=n.primaryColor,i=n.secondaryBackgroundColor);var c={height:40,backgroundColor:a,paddingTop:10,flex:1,cursor:"pointer"};return o.a.createElement("div",{style:{width:250,margin:0,padding:0,backgroundColor:i,borderRadius:12}},o.a.createElement("div",{style:{height:170,overflowY:"scroll",borderRadius:10,paddingLeft:10}},r),o.a.createElement("div",{style:{flexDirection:"row",display:"flex"}},o.a.createElement("div",{style:Object(l.a)(Object(l.a)({},c),{},{borderTopLeftRadius:10,marginRight:2}),onClick:function(){return e.onSelect(!1)}},o.a.createElement("p",{style:{fontSize:15,textAlign:"center"}},"deselect all")),o.a.createElement("div",{style:Object(l.a)(Object(l.a)({},c),{},{borderTopRightRadius:10,marginLeft:2}),onClick:function(){return e.onSelect(!0)}},o.a.createElement("p",{style:{fontSize:15,textAlign:"center"}},"select all"))),o.a.createElement("div",{style:Object(l.a)(Object(l.a)({},c),{},{borderBottomRightRadius:10,borderBottomLeftRadius:10,marginTop:4}),onClick:function(){return e.onFilter()}},o.a.createElement("p",{style:{paddingLeft:15,fontSize:15,textAlign:"center"}},"filter")))},e.onClicked=function(t,r){t[r].selected=!t[r].selected,e.setState({types:t}),e.forceUpdate()},e.onFilter=function(){u.a.setComponentValue(e.state.types),e.forceUpdate()},e.onSelect=function(t){e.state.types.forEach((function(e){e.selected=t})),e.forceUpdate()},e}return Object(c.a)(r)}(u.b),f=Object(u.c)(b);i.a.render(o.a.createElement(o.a.StrictMode,null,o.a.createElement(f,null)),document.getElementById("root"))}},[[16,1,2]]]);
//# sourceMappingURL=main.b79298d2.chunk.js.map