function [errorCode, GroupStatusString] = GroupStatusStringGet(socketId, GroupStatusCode)
%GroupStatusStringGet :  Return the group status string corresponding to the group status code
%
%	[errorCode, GroupStatusString] = GroupStatusStringGet(socketId, GroupStatusCode)
%
%	* Input parameters :
%		int32 socketId
%		int32 GroupStatusCode
%	* Output parameters :
%		int32 errorCode
%		cstring GroupStatusString


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
GroupStatusString = '';
for i = 1:103
	GroupStatusString = [GroupStatusString '          '];
end

% lib call
[errorCode, GroupStatusString] = calllib('XPS_Q8_drivers', 'GroupStatusStringGet', socketId, GroupStatusCode, GroupStatusString);
