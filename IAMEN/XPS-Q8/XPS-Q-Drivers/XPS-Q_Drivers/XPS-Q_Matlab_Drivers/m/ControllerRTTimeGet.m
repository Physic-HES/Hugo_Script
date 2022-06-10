function [errorCode, CurrentRTPeriod, CurrentRTUsage] = ControllerRTTimeGet(socketId)
%ControllerRTTimeGet :  Get controller corrector period and calculation time
%
%	[errorCode, CurrentRTPeriod, CurrentRTUsage] = ControllerRTTimeGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		doublePtr CurrentRTPeriod
%		doublePtr CurrentRTUsage


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
CurrentRTPeriod = 0;
CurrentRTUsage = 0;

% lib call
[errorCode, CurrentRTPeriod, CurrentRTUsage] = calllib('XPS_C8_drivers', 'ControllerRTTimeGet', socketId, CurrentRTPeriod, CurrentRTUsage);
