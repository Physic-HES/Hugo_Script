function [errorCode, UserMaximumZZZTargetDifference] = TZTrackingUserMaximumZZZTargetDifferenceGet(socketId, GroupName)
%TZTrackingUserMaximumZZZTargetDifferenceGet :  Get user maximum ZZZ target difference for tracking control
%
%	[errorCode, UserMaximumZZZTargetDifference] = TZTrackingUserMaximumZZZTargetDifferenceGet(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode
%		doublePtr UserMaximumZZZTargetDifference


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
UserMaximumZZZTargetDifference = 0;

% lib call
[errorCode, GroupName, UserMaximumZZZTargetDifference] = calllib('XPS_C8_drivers', 'TZTrackingUserMaximumZZZTargetDifferenceGet', socketId, GroupName, UserMaximumZZZTargetDifference);
