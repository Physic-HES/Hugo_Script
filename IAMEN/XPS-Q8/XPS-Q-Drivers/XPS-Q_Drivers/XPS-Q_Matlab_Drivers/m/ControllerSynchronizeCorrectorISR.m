function [errorCode] = ControllerSynchronizeCorrectorISR(socketId, ModeString)
%ControllerSynchronizeCorrectorISR :  Synchronize controller corrector ISR
%
%	[errorCode] = ControllerSynchronizeCorrectorISR(socketId, ModeString)
%
%	* Input parameters :
%		int32 socketId
%		cstring ModeString
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, ModeString] = calllib('XPS_C8_drivers', 'ControllerSynchronizeCorrectorISR', socketId, ModeString);
