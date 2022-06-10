function [errorCode, FrequencyTicks] = TimerGet(socketId, TimerName)
%TimerGet :  Get a timer
%
%	[errorCode, FrequencyTicks] = TimerGet(socketId, TimerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring TimerName
%	* Output parameters :
%		int32 errorCode
%		int32Ptr FrequencyTicks


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
FrequencyTicks = 0;

% lib call
[errorCode, TimerName, FrequencyTicks] = calllib('XPS_Q8_drivers', 'TimerGet', socketId, TimerName, FrequencyTicks);
