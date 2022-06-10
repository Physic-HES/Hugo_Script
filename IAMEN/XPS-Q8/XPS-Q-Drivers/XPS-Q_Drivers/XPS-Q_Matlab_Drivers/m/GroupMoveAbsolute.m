function [errorCode] = GroupMoveAbsolute(socketId, GroupName, TargetPosition)
%GroupMoveAbsolute :  Do an absolute move
%
%	[errorCode] = GroupMoveAbsolute(socketId, GroupName, TargetPosition)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double TargetPosition
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Count the number of element in the API
[tmp, nbElement] = size(TargetPosition);

% lib call
[errorCode, GroupName] = calllib('XPS_Q8_drivers', 'GroupMoveAbsolute', socketId, GroupName, nbElement, TargetPosition);
