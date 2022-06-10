function [errorCode, CPUTemperature, CPUFanSpeed] = CPUTemperatureAndFanSpeedGet(socketId)
%CPUTemperatureAndFanSpeedGet :  Get raw encoder positions for single axis theta encoder
%
%	[errorCode, CPUTemperature, CPUFanSpeed] = CPUTemperatureAndFanSpeedGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		doublePtr CPUTemperature
%		doublePtr CPUFanSpeed


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
CPUTemperature = 0;
CPUFanSpeed = 0;

% lib call
[errorCode, CPUTemperature, CPUFanSpeed] = calllib('XPS_Q8_drivers', 'CPUTemperatureAndFanSpeedGet', socketId, CPUTemperature, CPUFanSpeed);
