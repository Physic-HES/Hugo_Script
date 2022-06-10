function [errorCode] = TimerSet(socketId, TimerName, FrequencyTicks)
%TimerSet :  Set a timer
%
%	[errorCode] = TimerSet(socketId, TimerName, FrequencyTicks)
%
%	* Input parameters :
%		int32 socketId
%		cstring TimerName
%		int32 FrequencyTicks
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, TimerName] = calllib('XPS_Q8_drivers', 'TimerSet', socketId, TimerName, FrequencyTicks);
