function [errorCode, Status] = GroupMotionStatusGet(socketId, GroupName, nbElement)
%GroupMotionStatusGet :  Return group or positioner status
%
%	[errorCode, Status] = GroupMotionStatusGet(socketId, GroupName, nbElement)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		int32 nbElement
%	* Output parameters :
%		int32 errorCode
%		int32Ptr Status


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Status = [];
for i = 1:nbElement
	Status = [Status 0];
end

% lib call
[errorCode, GroupName, Status] = calllib('XPS_Q8_drivers', 'GroupMotionStatusGet', socketId, GroupName, nbElement, Status);
