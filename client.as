﻿package {    import flash.display.MovieClip;    import flash.events.NetStatusEvent;    import flash.events.SecurityErrorEvent;    import flash.net.NetConnection;	import flash.net.Responder;    public class client extends MovieClip {		private var nc:NetConnection;				public function client(){			nc = new NetConnection();			nc.addEventListener(NetStatusEvent.NET_STATUS, netStatusHandler);			nc.addEventListener(SecurityErrorEvent.SECURITY_ERROR, securityErrorHandler);			nc.connect("http://localhost:8080/amf");		}		private function securityErrorHandler(event:NetStatusEvent):void {			trace("securityErrorHandler: " + event);		}				private function netStatusHandler(event:NetStatusEvent):void {			switch (event.info.code) {				case "NetConnection.Connect.Success":					nc.call('minesweeper/render', new Responder(						function(result){							trace(result);						},												function(error){							trace(error);						}					));					break;				default:					trace(event.info.code);					break;			}		}	}}