package {
	import flash.display.MovieClip;
	import flash.events.NetStatusEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.NetConnection;
	import flash.net.Responder;
	
	public class MinesweeperApp extends MovieClip {
		private var nc:NetConnection = null;
		
		public function MinesweeperApp(){
			trace('connecting');
			this.nc = new NetConnection();
			this.nc.addEventListener(NetStatusEvent.NET_STATUS, this.netStatus);
			this.nc.addEventListener(SecurityErrorEvent.SECURITY_ERROR, this.securityError);
			this.nc.connect("http:/amf");
		}
		
		public function securityError(event:SecurityErrorEvent):void {
			trace("securityErrorHandler: " + event);
		}
		
		public function netStatus(event:NetStatusEvent):void {
			trace('status: ' + event.info.code);
			switch (event.info.code) {
				case "NetConnection.Connect.Success":
					nc.call('minesweeper/render', new Responder(
						function(result){
							trace(result);
						},
						
						function(error){
							trace(error);
						}
					));
					break;
				default:
					trace(event.info.code);
					break;
			}
		}
	}
}