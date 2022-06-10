function [errorCode, Version] = FirmwareVersionGet(socketId)
%FirmwareVersionGet :  Return firmware version
%
%	[errorCode, Version] = FirmwareVersionGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring Version


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Version = '';
for i = 1:103
	Version = [Version '          '];
end

% lib call
[errorCode, Version] = calllib('XPS_Q8_drivers', 'FirmwareVersionGet', socketId, Version);
