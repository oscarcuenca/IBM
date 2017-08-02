function Service(appClient) {
  this.appClient = appClient;
  
}

Service.prototype.connect = function() {
  // TODO connect to iotf here with this.appClient
  this.appClient.connect();
  var that = this;
  this.appClient.on('connect', function() {
    // TODO hook up device events here with this.appClient
    that.appClient.subscribeToDeviceEvents("+","+","temperature");
    
  }.bind(this));

  this.appClient.on("deviceEvent", function (deviceType, deviceId, eventType, format, payload) {
	    var tempis = JSON.parse(payload);
	    var temp = parseFloat(tempis.d.temperature);
	    if (temp != process.env.temp) {
	      this.handleTempEvent(temp);
	    }
	  }.bind(this));

	};
	
	    var temp_old_init = 0
	    Service.prototype.handleTempEvent = function(temp) {
	 	   // handle temperature changes here and call this.warningOn/this.warningOff accordingly
	 	  var temp_old = temp_old_init || temp;
	 	  var temp_new = temp;
	 	  var limit = 29;

	 	  if (temp_old >= limit && temp_new < limit) {
	 	      this.warningOff();
	 	  } else if (temp_old < limit && temp_new >= limit) {
	 	      this.warningOn();
	 	  }

	 	  temp_old_init = temp_new;

	 	};
Service.prototype.warningOn = function() {
  // TODO send a device commmand here
  // warningOn should only be called when the warning isn't already on
	
	    var that = this;
	    var myData = {"screen":"on"};
	    myData = JSON.stringify(myData);
	    
	    that.appClient.publishDeviceCommand("SenseHAT","senb827eb7ddd6d","display","json",myData);
	    
	 
};

Service.prototype.warningOff = function() {
  // TODO send a device commmand here
  // warningOff should only be called when the warning isn't already off
	
	   var that = this;
	   
	    var myData = {"screen":"off"};
	    myData = JSON.stringify(myData);
	    
	    that.appClient.publishDeviceCommand("SenseHAT","senb827eb7ddd6d","display","json",myData);
	    

	
};

module.exports = Service;
