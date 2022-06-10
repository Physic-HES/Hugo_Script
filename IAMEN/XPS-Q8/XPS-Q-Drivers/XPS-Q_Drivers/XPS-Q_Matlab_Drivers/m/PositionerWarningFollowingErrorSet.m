function [errorCode] = PositionerWarningFollowingErrorSet(socketId, PositionerName, WarningFollowingError)
%PositionerWarningFollowingErrorSet :  Set positioner warning following error limit
%
%	[errorCode] = PositionerWarningFollowingErrorSet(socketId, PositionerName, WarningFollowingError)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double WarningFollowingError
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerWarningFollowingErrorSet', socketId, PositionerName, WarningFollowingError);
