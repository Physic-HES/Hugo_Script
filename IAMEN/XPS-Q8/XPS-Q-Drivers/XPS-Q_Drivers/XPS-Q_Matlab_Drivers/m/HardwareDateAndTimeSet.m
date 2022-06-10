function [errorCode] = HardwareDateAndTimeSet(socketId, DateAndTime)
%HardwareDateAndTimeSet :  Set hardware date and time
%
%	[errorCode] = HardwareDateAndTimeSet(socketId, DateAndTime)
%
%	* Input parameters :
%		int32 socketId
%		cstring DateAndTime
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, DateAndTime] = calllib('XPS_Q8_drivers', 'HardwareDateAndTimeSet', socketId, DateAndTime);
