function [errorCode] = FocusProcessSocketReserve(socketId)
%FocusProcessSocketReserve :  Set user maximum ZZZ target difference for tracking control
%
%	[errorCode] = FocusProcessSocketReserve(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode] = calllib('XPS_C8_drivers', 'FocusProcessSocketReserve', socketId);
