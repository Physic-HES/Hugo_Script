function [errorCode] = GroupMoveAbortFast(socketId, GroupName, AccelerationMultiplier)
%GroupMoveAbortFast :  Abort quickly a move
%
%	[errorCode] = GroupMoveAbortFast(socketId, GroupName, AccelerationMultiplier)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		int32 AccelerationMultiplier
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName] = calllib('XPS_C8_drivers', 'GroupMoveAbortFast', socketId, GroupName, AccelerationMultiplier);
