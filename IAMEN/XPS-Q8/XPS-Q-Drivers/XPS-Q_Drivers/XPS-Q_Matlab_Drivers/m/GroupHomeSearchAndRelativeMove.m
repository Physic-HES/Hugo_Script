function [errorCode] = GroupHomeSearchAndRelativeMove(socketId, GroupName, TargetDisplacement)
%GroupHomeSearchAndRelativeMove :  Start home search sequence and execute a displacement
%
%	[errorCode] = GroupHomeSearchAndRelativeMove(socketId, GroupName, TargetDisplacement)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double TargetDisplacement
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Count the number of element in the API
[tmp, nbElement] = size(TargetDisplacement);

% lib call
[errorCode, GroupName] = calllib('XPS_Q8_drivers', 'GroupHomeSearchAndRelativeMove', socketId, GroupName, nbElement, TargetDisplacement);
