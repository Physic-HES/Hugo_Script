function [errorCode, DateAndTime] = HardwareDateAndTimeGet(socketId)
%HardwareDateAndTimeGet :  Return hardware date and time
%
%	[errorCode, DateAndTime] = HardwareDateAndTimeGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring DateAndTime


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
DateAndTime = '';
for i = 1:103
	DateAndTime = [DateAndTime '          '];
end

% lib call
[errorCode, DateAndTime] = calllib('XPS_Q8_drivers', 'HardwareDateAndTimeGet', socketId, DateAndTime);
