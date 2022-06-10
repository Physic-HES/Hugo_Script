function [errorCode] = TZTrackingUserMaximumZZZTargetDifferenceSet(socketId, GroupName, UserMaximumZZZTargetDifference)
%TZTrackingUserMaximumZZZTargetDifferenceSet :  Set user maximum ZZZ target difference for tracking control
%
%	[errorCode] = TZTrackingUserMaximumZZZTargetDifferenceSet(socketId, GroupName, UserMaximumZZZTargetDifference)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double UserMaximumZZZTargetDifference
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName] = calllib('XPS_C8_drivers', 'TZTrackingUserMaximumZZZTargetDifferenceSet', socketId, GroupName, UserMaximumZZZTargetDifference);
