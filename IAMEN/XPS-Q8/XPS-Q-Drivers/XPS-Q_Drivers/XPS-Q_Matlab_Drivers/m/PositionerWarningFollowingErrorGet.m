function [errorCode, WarningFollowingError] = PositionerWarningFollowingErrorGet(socketId, PositionerName)
%PositionerWarningFollowingErrorGet :  Get positioner warning following error limit
%
%	[errorCode, WarningFollowingError] = PositionerWarningFollowingErrorGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr WarningFollowingError


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
WarningFollowingError = 0;

% lib call
[errorCode, PositionerName, WarningFollowingError] = calllib('XPS_C8_drivers', 'PositionerWarningFollowingErrorGet', socketId, PositionerName, WarningFollowingError);
