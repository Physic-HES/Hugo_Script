function [errorCode, GroupStatusList] = GroupStatusListGet(socketId)
%GroupStatusListGet :  Group status list
%
%	[errorCode, GroupStatusList] = GroupStatusListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring GroupStatusList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
GroupStatusList = '';
for i = 1:6554
	GroupStatusList = [GroupStatusList '          '];
end

% lib call
[errorCode, GroupStatusList] = calllib('XPS_Q8_drivers', 'GroupStatusListGet', socketId, GroupStatusList);
