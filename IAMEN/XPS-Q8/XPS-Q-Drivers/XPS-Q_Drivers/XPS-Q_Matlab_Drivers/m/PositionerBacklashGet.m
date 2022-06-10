function [errorCode, BacklashValue, BacklaskStatus] = PositionerBacklashGet(socketId, PositionerName)
%PositionerBacklashGet :  Read backlash value and status
%
%	[errorCode, BacklashValue, BacklaskStatus] = PositionerBacklashGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr BacklashValue
%		cstring BacklaskStatus


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
BacklashValue = 0;
BacklaskStatus = '';
for i = 1:103
	BacklaskStatus = [BacklaskStatus '          '];
end

% lib call
[errorCode, PositionerName, BacklashValue, BacklaskStatus] = calllib('XPS_Q8_drivers', 'PositionerBacklashGet', socketId, PositionerName, BacklashValue, BacklaskStatus);
