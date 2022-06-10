function [errorCode] = TZFocusModeDisable(socketId, GroupName)
%TZFocusModeDisable :  Disable the focus mode
%
%	[errorCode] = TZFocusModeDisable(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName] = calllib('XPS_C8_drivers', 'TZFocusModeDisable', socketId, GroupName);
