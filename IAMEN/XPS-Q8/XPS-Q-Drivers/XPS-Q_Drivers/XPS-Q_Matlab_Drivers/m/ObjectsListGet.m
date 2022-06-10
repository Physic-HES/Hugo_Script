function [errorCode, ObjectsList] = ObjectsListGet(socketId)
%ObjectsListGet :  Group name and positioner name
%
%	[errorCode, ObjectsList] = ObjectsListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring ObjectsList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ObjectsList = '';
for i = 1:6554
	ObjectsList = [ObjectsList '          '];
end

% lib call
[errorCode, ObjectsList] = calllib('XPS_Q8_drivers', 'ObjectsListGet', socketId, ObjectsList);
