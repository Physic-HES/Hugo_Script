function [errorCode, Status] = GroupStatusGet(socketId, GroupName)
%GroupStatusGet :  Return group status
%
%	[errorCode, Status] = GroupStatusGet(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
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
Status = 0;

% lib call
[errorCode, GroupName, Status] = calllib('XPS_Q8_drivers', 'GroupStatusGet', socketId, GroupName, Status);
