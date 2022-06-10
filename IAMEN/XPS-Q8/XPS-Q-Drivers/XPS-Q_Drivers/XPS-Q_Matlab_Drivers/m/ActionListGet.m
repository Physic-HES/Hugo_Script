function [errorCode, ActionList] = ActionListGet(socketId)
%ActionListGet :  Action list
%
%	[errorCode, ActionList] = ActionListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring ActionList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ActionList = '';
for i = 1:205
	ActionList = [ActionList '          '];
end

% lib call
[errorCode, ActionList] = calllib('XPS_Q8_drivers', 'ActionListGet', socketId, ActionList);
